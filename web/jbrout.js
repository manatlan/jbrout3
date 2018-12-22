var basename=function(path) {return path.split(/[\\/]/).pop()}
var dirname=function(path) {return path.replace(/\\/g,'/').replace(/\/[^\/]*$/, '')}

Vue.filter("basename", path => basename(path) )
Vue.filter("dirname", path => basename(dirname(path)) ) // in fact its basename(dirname)
Vue.filter("date", s => s.substr(0,4)+"/"+s.substr(4,2)+"/"+s.substr(6,2)+" "+s.substr(8,2)+":"+s.substr(10,2)+":"+s.substr(12,2) ) // in fact its basename(dirname)

var bus=new Vue();

var notImplemented=function() {alert("not implemented")}

wuy.on("set-info", (idx,path,info)=>mystore.dispatch("setInfo",{idx,path,info}) )
wuy.on("set-working", (msg)=>mystore.dispatch("working",msg) )
var CACHE={} // <- this things is here, just because browser CACHEs "http get jpg"
             //    so it breaks the "set-info" system, and in that case
             //    the vue app get info from here, for cached jpeg.

var log=console.log;


async function asyncForEach(context,array, callback) {
  context.dispatch("working","0/"+(array.length));
  for (let index = 0; index < array.length; index++) {
    context.dispatch("working",index+"/"+(array.length));
    await callback(array[index], index, array);
  }
  context.dispatch("working",null);
}


document.addEventListener('keydown', function(evt) {
  var catsh=false;
  if(mystore.state.working!=null) return; // no keyboard when working
  
  if(evt.ctrlKey) {
      if(evt.key=="l") { var p=(mystore.getters.photo!=null?mystore.getters.photo.path:null); mystore.dispatch('photoRotateLeft',p); catsh=true}
      if(evt.key=="r") { var p=(mystore.getters.photo!=null?mystore.getters.photo.path:null); mystore.dispatch('photoRotateRight',p) ; catsh=true}
      if(evt.key=="t") { var p=(mystore.getters.photo!=null?mystore.getters.photo.path:null); mystore.dispatch('photoRebuildThumbnail',p) ; catsh=true}
      if(evt.key=="a") { mystore.dispatch('selectAll');catsh=true}
  }
  else {
    if(evt.code=="ArrowRight") { mystore.dispatch("view","next"); catsh=true }
    if(evt.code=="ArrowDown") { mystore.dispatch("view","next"); catsh=true }
    if(evt.code=="ArrowLeft") { mystore.dispatch("view","previous"); catsh=true }
    if(evt.code=="ArrowUp") { mystore.dispatch("view","previous"); catsh=true }
    if(evt.code=="Escape") { mystore.dispatch("view",null); catsh=true }
    if(evt.code=="Space") { mystore.dispatch("switchBasket"); catsh=true }
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
    years:[],
    working:null,
    dragging: null,
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
    working: function(context,txt) {
      context.state.working=txt;
    },
    dragging: function(context,txt) {
      context.state.dragging=txt;
    },
    init: async function(context) {
      log("*init")
      context.state.files=[];
      context.state.selected=[];
      context.state.basket=await wuy.selectFromBasket();
      context.state.folders=await wuy.getFolders();
      context.state.tags=await wuy.getTags();
      context.state.displayType=await wuy.cfgGet("displayType","name")
      context.state.orderReverse=await wuy.cfgGet("orderReverse",false)
    },
    getYears: async function(context) {
      log("*getYears")
      context.state.years=await wuy.getYears();
      context.state.years.reverse();
    },
    getYear: async function(context,year) {
      log("*getYear",year)
      var ll=await wuy.getYear(year);
      context.dispatch( "_feedFiles", ll )
    },
    selectAlbum: async function(context,{path,all}) {
      log("*selectAlbum",path)
      var ll=await wuy.selectFromFolder(path,all)
      context.dispatch( "_feedFiles", ll )
      bus.$emit("select-path",path)
    },
    refreshAlbum: async function(context,path) {
      log("*refreshAlbum",path)
      await wuy.refreshFolder(path)
      context.dispatch( "selectAlbum", {path,all:true} )
      context.state.files.forEach( i=>bus.$emit("change-photo",i.path) )
      context.state.folders=await wuy.getFolders();
      context.state.tags=await wuy.getTags();
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
      context.state.basket=await wuy.selectFromBasket()
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

      if(context.state.viewerIdx!=null)
        context.dispatch( "selectJustOne", context.state.files[context.state.viewerIdx].path )
        
    },
    selectTags: async function(context,tags) {
      log("*selectTags",tags)
      if(tags.length>0) {
        var ll=await wuy.selectFromTags(tags)
        context.dispatch( "_feedFiles", ll )
      }
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
        if(context.state.files[obj.idx])
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
        asyncForEach(context,context.state.selected, async (p,idx)=>{
          await context.dispatch("photoRebuildThumbnail",p)
        })
    },
    photoRotateRight: async function(context,path) {
      log("*photoRotateRight",path)
      if(path) {
        await wuy.photoRotateRight(path)
        bus.$emit("change-photo",path)
      }
      else
        asyncForEach(context,context.state.selected, async (p,idx)=>{
          await context.dispatch("photoRotateRight",p)
        })

    },
    photoRotateLeft: async function(context,path) {
      log("*photoRotateLeft",path)
      if(path) {
        await wuy.photoRotateLeft(path)
        bus.$emit("change-photo",path)
      }
      else
        asyncForEach(context,context.state.selected, async (p,idx)=>{
          await context.dispatch("photoRotateLeft",p)
        })
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
    switchBasket: async function(context) {
      log("*switchBasket")
      context.state.selected.forEach( p=>{
        var isInBasket=context.getters.basket.indexOf(p)>=0;
        context.dispatch("photoBasket",{path:p,bool:!isInBasket})
      });
    },

    photoAddTags: async function(context,{path,tags}) {
      log("*photoAddTags",path,tags)
      if(path) {
        await wuy.photoAddTags(path,tags)
        bus.$emit("change-photo",path)
      }
      else
        context.state.selected.forEach( p=>context.dispatch("photoAddTags",{path:p,tags}) )
    },
    photoClearTags: async function(context,path) {
      log("*photoClearTags",path)
      if(path) {
        await wuy.photoClearTags(path)
        bus.$emit("change-photo",path)
      }
      else
      context.state.selected.forEach( p=>context.dispatch("photoClearTags",p) )
    },
    photoDelTag: async function(context,tag) {
      log("*photoDelTag",tag)
      context.state.selected.forEach( async p=>{
        await wuy.photoDelTag(p,tag)
        bus.$emit("change-photo",p)
      })
    },
    photoMoveAlbum: async function(context,path) { //TODO: finnish here
      log("*photoMoveAlbum",path)
      alert("NOT DONE : will move "+context.state.selected.length+"selected to "+path)
    },
    albumMoveAlbum: async function(context,{path1,path2}) { //TODO: finnish here
      log("*albumMoveAlbum",path1,path2)
      alert("NOT DONE : will move "+path1+" to "+path2)
    },


    // uiLeftTags ...
    //==================================================
    tagsAddTag: async function(context,cat) {
      log("*tagsAddTag")
      var txt=prompt("New Tag under '"+cat+"' ?")
      if(txt) {
        var ok=await wuy.tagsAddTag(cat,txt)
        if(ok) context.state.tags=await wuy.getTags();
      }
    },
    tagsAddCat: async function(context,cat) {
      log("*tagsAddCat")
      var txt=prompt("New Category under '"+cat+"' ?")
      if(txt) {
        var ok=await wuy.tagsAddCat(cat,txt)
        if(ok) context.state.tags=await wuy.getTags();
      }
    },
    tagsDelTag: async function(context,txt) {
      log("*tagsDelTag",txt)
      var ll=await wuy.selectFromTags([txt])
      if(ll.length>0)
        alert("Tag is in use, can't be deleted")
      else {
        var ok=await wuy.tagsDelTag(txt)
        if(ok) context.state.tags=await wuy.getTags();
      }
    },
    tagsDelCat: async function(context,{cat,tags}) {
      log("*tagsDelCat",cat)
      var ll=await wuy.selectFromTags(tags)
      if(ll.length>0)
        alert("Category is in use, can't be deleted")
      else {
        var ok=await wuy.tagsDelCat(cat)
        if(ok) context.state.tags=await wuy.getTags();
      }
    },
    tagMoveToCat: async function(context,{tag,cat}) {
      log("*tagMoveToCat",tag,cat)
      var ok=await wuy.tagMoveToCat(tag,cat)
      if(ok) context.state.tags=await wuy.getTags();
    },
    catMoveToCat: async function(context,{cat1,cat2}) {
      log("*catMoveToCat",cat1,cat2)
      var ok=await wuy.catMoveToCat(cat1,cat2)
      if(ok) context.state.tags=await wuy.getTags();
    },

    // uiTop ...
    //==================================================
    addFolder: async function(context) {
      log("*addFolder")
      context.dispatch("working","Select folder to add in")
      var ok=await wuy.addFolder()
      context.dispatch("working",null)
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
    selectAll: function(context) {
      log("*selectAll")
      context.state.selected = context.state.files.map( i=>i.path )
    },
    selectJustOne: function(context,obj) {
      log("*selectJustOne",obj)
      context.state.selected=[obj]
    },
    selectSwitchOne: function(context,obj) {
      log("*selectSwitchOne",obj)
      var idx=context.state.selected.indexOf(obj);
      if(idx>=0)
        context.state.selected.splice(idx, 1)
      else
        context.state.selected.push(obj)
    },
    selectAddOne: function(context,obj) {
      log("*selectAddOne",obj)
      var idx=context.state.selected.indexOf(obj);
      if(idx<0)
        context.state.selected.push(obj)
    },
}
})

Vue.prototype.$myapi = {};  // just for example

wuy.init( function() {new Vue({el:"#jbrout",store:mystore})} )




