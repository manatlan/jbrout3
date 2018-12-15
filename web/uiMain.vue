<template>
    <div @contextmenu.prevent="menu" @scroll="scroll()">

        <thumb v-for="(i,idx) in list" :key="idx"
            @allclick="click($event,i,idx)"
            @dblclick="dblclick($event,i,idx)"
            :value="i"
            :class="$store.state.selected.indexOf(i.path)>=0?'selected':''"
        ></thumb>

    </div>
</template>
<script>
export default {
    data: function() {
        return {
            currentIndex: null,
            list: [],
        }
    },
    created() {
        bus.$on("change-set-photos",()=>{
            this.$el.scrollTop=0;
            this.list=[]
            this.feed(60)
        })
    },
    methods: {
        feed(nb) {
          var tot=this.list.length;
          if(tot<this.$store.state.files.length)
            for(var n=tot;n<=tot+nb;n++)
              if(this.$store.state.files[n]) this.list.push( this.$store.state.files[n] )
        },
        scroll () {
          if(this.$el.scrollTop+this.$el.clientHeight+200 >=this.$el.scrollHeight)
            this.feed(10)
        },
        dblclick(event,item,idx) {
            this.$root.$refs.viewer.view(idx)
        },
        click(event,item,idx) {

            if(event.shiftKey==true && event.button==0) {
                var ll= [this.currentIndex,idx]
                ll.sort()
                for(var i=ll[0];i<=ll[1];i++)
                    this.$store.dispatch('selectAddOne',this.$store.state.files[i].path )
            }
            else if(event.ctrlKey==true || event.button==1)
                this.$store.dispatch('selectSwitchOne',item.path)
            else
                this.$store.dispatch('selectJustOne',item.path)

            this.currentIndex=idx
        },
        menu(e) {
            var menu = [];

            if(this.$store.state.selected.length>0)
                menu.push(    {name:'Add to basket', callback: notImplemented } )
            if(this.$store.state.selected.length==1) {
                menu.push(    {name:'Select this album', callback: notImplemented } )
                menu.push(    {name:'Select this time', callback: notImplemented } )
            }
            if(this.$store.state.selected.length>0) {
                menu.push(    {name:'op> rotate left', callback: notImplemented } )
                menu.push(    {name:'op> rotate right', callback: notImplemented } )
                menu.push(    {name:'op> change date', callback: notImplemented } )
                menu.push(    {name:'op> rebuild thumbnail', callback: notImplemented } )
                menu.push(    {name:'op> comment', callback: notImplemented } )
                menu.push(    {name:'Delete', callback: notImplemented } )
            }
            if(menu.length>0)
                this.$root.$refs.menu.pop(menu,e)
        },

    },
    watch: {
        //~ '$store.state.files':function (to, from) {
            //~ this.$el.scrollTop=0;
            //~ Vue.nextTick( this.refreshDataSrc);
        //~ },
    }
}
</script>
<style scoped>
    :scope {
        overflow-y: auto;
        background:white;
        padding:4px;
        display:flex;
        flex-flow: row wrap;
        align-content: flex-start;
    }
    :scope > * {
        flex: 0 0 auto;
        width:160px;    /*TODO: not top*/
        height:160px;   /*TODO: not top*/
    }
    .selected {background:yellow}
</style>
<style>
.click {cursor:pointer}
</style>
