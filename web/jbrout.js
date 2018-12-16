Vue.filter("basename", path => {return path.split(/[\\/]/).pop()} )
Vue.filter("dirname", path => {return path.replace(/\\/g,'/').replace(/\/[^\/]*$/, '').split(/[\\/]/).pop()} ) // in fact its basename(dirname)

var bus=new Vue();

var notImplemented=function() {alert("not implemented")}

wuy.on("set-info", (idx,path,info)=>mystore.dispatch("setInfo",{idx,path,info}) )
var CACHE={}
var log=console.log;


document.addEventListener('keydown', function(evt) {
  var catsh=false;
  if(evt.ctrlKey) {
      if(evt.code=="KeyL") { var p=(mystore.getters.photo!=null?mystore.getters.photo.path:null); mystore.dispatch('photoRotateLeft',p); catsh=true}
      if(evt.code=="KeyR") { var p=(mystore.getters.photo!=null?mystore.getters.photo.path:null); mystore.dispatch('photoRotateRight',p) ; catsh=true}
      if(evt.code=="KeyT") { var p=(mystore.getters.photo!=null?mystore.getters.photo.path:null); mystore.dispatch('photoRebuildThumbnail',p) ; catsh=true}
  }
  else {
    if(evt.code=="ArrowRight") { mystore.dispatch("view","next"); catsh=true }    
    if(evt.code=="ArrowDown") { mystore.dispatch("view","next"); catsh=true }    
    if(evt.code=="ArrowLeft") { mystore.dispatch("view","previous"); catsh=true }    
    if(evt.code=="ArrowUp") { mystore.dispatch("view","previous"); catsh=true }    
    if(evt.code=="Escape") { mystore.dispatch("view",null); catsh=true }    
  }

  if(catsh) {
    evt.preventDefault();
    evt.stopPropagation(); 
    return false
  }
})


var mystore = new Vuex.Store({
  state: {
    folders: [],         // tree
    tags: [],            // tree
    files: [],           // list of photonodes/json
    basket: [],           // list of photonodes/json
    selected:[],         // list of path
    displayType: "name", // "name", "date", "tags","album","comment"
    orderReverse:false,
    viewerIdx:null,
  },
  getters: {
      photo(state) {
          if(state.viewerIdx!=null)
            return state.files[state.viewerIdx]
          else
            return null;
      },
      basket(state) {
        return state.basket.map( p=>p.path )
      },
  },
  // NO MUTATIONS (all in actions)
  actions: {
    init: async function(context) {
      log("*init")
      context.state.files=[];
      context.state.selected=[];
      context.state.basket=await wuy.selectFromBasket();
      console.log("BASK",context.getters.basket)
      context.state.folders=await wuy.getFolders();
      context.state.tags=await wuy.getTags();
      context.state.displayType=await wuy.cfgGet("displayType","name")
      context.state.orderReverse=await wuy.cfgGet("orderReverse",false)
    },
    selectAlbum: async function(context,{path,all}) {
      log("*selectAlbum",path)
      var ll=await wuy.selectFromFolder(path,all)
      context.dispatch( "_feedFiles", ll )
    },
    refreshAlbum: async function(context,path) {
      log("*refreshAlbum",path)
      await wuy.refreshFolder(path)
      context.dispatch( "selectAlbum", {path,all:true} )
      context.state.files.forEach( i=>bus.$emit("change-photo",i.path))
      context.state.folders=await wuy.getFolders();
    },
    removeBasket: async function(context,path) {
      log("*removeBasket",path)
      await wuy.removeBasket()
      context.state.basket=await wuy.selectFromBasket()
    },
    removeAlbum: async function(context,path) {
      log("*removeAlbum",path)
      await wuy.removeFolder(path)
      context.dispatch( "_feedFiles", [] )
      context.state.folders=await wuy.getFolders();
    },
    view: function(context,idx) {
      log("*view",idx)
      if(context.state.viewerIdx!=null && idx=="next") {
          context.state.viewerIdx+=1
          context.state.viewerIdx=(context.state.files.length+context.state.viewerIdx)%context.state.files.length;
      }
      else if (context.state.viewerIdx!=null && idx=="previous") {
          context.state.viewerIdx+=-1
          context.state.viewerIdx=(context.state.files.length+context.state.viewerIdx)%context.state.files.length;
      }
      else
        context.state.viewerIdx=idx;
    },
    selectTags: async function(context,tags) {
      log("*selectTags",tags)
      var ll=await wuy.selectFromTags(tags)
      context.dispatch( "_feedFiles", ll )
    },
    selectBasket: async function(context) {
      log("*selectBasket")
      context.dispatch( "_feedFiles", context.state.basket )
    },
    _feedFiles: function(context,ll) {
      log("*_feedFiles",ll.length)
      context.state.selected=[];
      ll.sort( (a,b)=>parseInt(a.date) - parseInt(b.date) );
      if(context.state.orderReverse) ll=ll.reverse();

      //~ context.state.files=photoNodes(ll);

      context.state.files=ll;
      context.state.files.forEach( (item,idx)=>{
        if (item.path in CACHE) context.dispatch( "setInfo", {idx:idx,path:item.path,info:CACHE[item.path]} )
      })

      bus.$emit("change-set-photos")
    },
    setInfo: async function(context,obj) {
      // log("*setInfo",obj)
      CACHE[obj.path]=obj.info
      for(var k of Object.keys(obj.info)) {
        Vue.set(context.state.files[obj.idx],k,obj.info[k])
      }
    },

    photoRebuildThumbnail: async function(context,path) {
      log("*photoRebuildThumbnail",path)
      if(path) {
        await wuy.photoRebuildThumbnail(path)
        bus.$emit("change-photo",path)
      }
      else
        context.state.selected.forEach( p=>context.dispatch("photoRebuildThumbnail",p))
    },
    photoRotateRight: async function(context,path) {
      log("*photoRotateRight",path)
      if(path) {
        await wuy.photoRotateRight(path)
        bus.$emit("change-photo",path)
      }
      else
        context.state.selected.forEach( p=>context.dispatch("photoRotateRight",p))
    },
    photoRotateLeft: async function(context,path) {
      log("*photoRotateLeft",path)
      if(path) {
        await wuy.photoRotateLeft(path)
        bus.$emit("change-photo",path)
      }
      else
        context.state.selected.forEach( p=>context.dispatch("photoRotateLeft",p))
    },
    photoBasket: async function(context,{path,bool}) {
      log("*photoBasket",path,bool)
      if(path) {
        await wuy.photoBasket(path,bool)
        context.state.basket=await wuy.selectFromBasket();
      }
      else
        context.state.selected.forEach( p=>context.dispatch("photoBasket",{path:p,bool}))

    },


    // uiTop ...
    //==================================================
    addFolder: async function(context) {
      log("*addFolder")
      var ok=await wuy.addFolder()
      if(ok) await context.dispatch( "init" )
    },
    setOrderReverse: function(context,bool) {
      log("*setOrderReverse",bool)
      context.state.orderReverse=bool;
      var ll=context.state.files;
      context.dispatch( "_feedFiles", ll )
      wuy.cfgSet("orderReverse",bool)
    },
    setDisplayType: function(context,displayType) {
      log("*setDisplayType",displayType)
      context.state.displayType=displayType;
      wuy.cfgSet("displayType",displayType)
    },

    // uiMain ...
    //==================================================
    selectJustOne: function(context,obj) {
      context.state.selected=[obj]
    },
    selectSwitchOne: function(context,obj) {
      var idx=context.state.selected.indexOf(obj);
      if(idx>=0)
        context.state.selected.splice(idx, 1)
      else
        context.state.selected.push(obj)
    },
    selectAddOne: function(context,obj) {
      var idx=context.state.selected.indexOf(obj);
      if(idx<0)
        context.state.selected.push(obj)
    },
}
})

Vue.prototype.$myapi = {};  // just for example

wuy.init( function() {new Vue({el:"#jbrout",store:mystore})} )




