Vue.filter("basename", path => {return path.split(/[\\/]/).pop()} )
Vue.filter("dirname", path => {return path.replace(/\\/g,'/').replace(/\/[^\/]*$/, '').split(/[\\/]/).pop()} ) // in fact its basename(dirname)

var bus=new Vue();

var notImplemented=function() {alert("not implemented")}

wuy.on("set-info", (idx,path,info)=>mystore.dispatch("setInfo",{idx,path,info}) )
var CACHE={}

var log=console.log;

var mystore = new Vuex.Store({
  state: {
    folders: [],         // tree
    tags: [],            // tree
    files: [],           // list of photonodes/json
    selected:[],         // list of path
    displayType: "name", // "name", "date", "tags","album","comment"
    orderReverse:false,
  },
  getters: {
      nimp() {                 // just for example
          return state.title;
      },
  },
  // NO MUTATIONS (all in actions)
  actions: {
    init: async function(context) {
      log("*init")
      context.state.files=[];
      context.state.selected=[];
      context.state.folders=await wuy.getFolders();
      context.state.tags=await wuy.getTags();
    },
    selectAlbum: async function(context,{path,all}) {
      log("*selectAlbum",path)
      var ll=await wuy.selectFromFolder(path,all)
      context.dispatch( "_feedFiles", ll )
    },
    selectTags: async function(context,tags) {
      log("*selectTags",tags)
      var ll=await wuy.selectFromTags(tags)
      context.dispatch( "_feedFiles", ll )
    },
    selectBasket: async function(context) {
      log("*selectBasket")
      var ll=await wuy.selectFromBasket()
      context.dispatch( "_feedFiles", ll )
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
      await wuy.photoRebuildThumbnail(path)
      bus.$emit("change-photo",path)
    },
    photoRotateRight: async function(context,path) {
      log("*photoRotateRight",path)
      await wuy.photoRotateRight(path)
      bus.$emit("change-photo",path)
    },
    photoRotateLeft: async function(context,path) {
      log("*photoRotateLeft",path)
      await wuy.photoRotateLeft(path)
      bus.$emit("change-photo",path)
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
    },
    setDisplayType: function(context,displayType) {
      log("*setDisplayType",displayType)
      context.state.displayType=displayType;
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




