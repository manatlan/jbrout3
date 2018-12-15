Vue.filter("basename", path => {return path.split(/[\\/]/).pop()} )
Vue.filter("dirname", path => {return path.replace(/\\/g,'/').replace(/\/[^\/]*$/, '').split(/[\\/]/).pop()} ) // in fact its basename(dirname)

var bus=new Vue();

var notImplemented=function() {alert("not implemented")}

var photoNodes=function(ll) {
    var PROPS=["comment","rating","resolution","tags"];

    var feed=function( orig ) {
        wuy.getInfo(orig.path).then( more => {
          for(var o of Object.keys(more)) {
            Vue.set(orig,o,more[o])
          }
        })
    }
    //~ return ll.map( item => {
        //~ return {
          //~ path: item.path,
          //~ date: item.date,
          //~ tags: [],
          //~ comment: "",
          //~ resolution: "",
          //~ rating: 0,
        //~ }
    //~ });
    return ll.map( item => {
        return new Proxy( item, {
            tags: [],
            get: function(target, propKey){
                if(!target.hasOwnProperty(propKey)) {
                    if( PROPS.includes(propKey)) feed(target)
                }
                return target[propKey];
            },
        })
    });
}

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
    init: async function(context,obj) {
      context.state.files=[];
      context.state.selected=[];
      context.state.folders=await wuy.getFolders();
      context.state.tags=await wuy.getTags();
    },
    selectAlbum: async function(context,{path,all}) {
      var ll=await wuy.selectFromFolder(path,all)
      context.dispatch( "_feedFiles", ll )
    },
    selectTags: async function(context,tags) {
      var ll=await wuy.selectFromTags(tags)
      context.dispatch( "_feedFiles", ll )
    },
    selectBasket: async function(context) {
      var ll=await wuy.selectFromBasket()
      context.dispatch( "_feedFiles", ll )
    },
    _feedFiles: function(context,ll) {
      context.state.selected=[];
      ll.sort( (a,b)=>parseInt(a.date) - parseInt(b.date) );
      if(context.state.orderReverse) ll=ll.reverse();

      context.state.files=photoNodes(ll);
      bus.$emit("change-set-photos")
    },

    // uiTop ...
    //==================================================
    addFolder: async function(context) {
      var ok=await wuy.addFolder()
      if(ok) await context.dispatch( "init" )
    },
    setOrderReverse: function(context,bool) {
      context.state.orderReverse=bool;
      var ll=context.state.files;
      context.dispatch( "_feedFiles", ll )
    },
    setDisplayType: function(context,displayType) {
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




