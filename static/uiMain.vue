<template>
    <div @scroll="scroll()" @contextmenu.prevent="">

        <thumb v-for="(i,idx) in list" :key="idx"
            @allclick="click($event,i,idx)"
            @dblclick="dblclick($event,i,idx)"
            @menu="menu($event,i,idx)"
            :value="i"
            :idx="idx"
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
    beforeMount() {
        bus.$on("change-set-photos",()=>{
            log("event change-set-photos")
            this.$el.scrollTop=0;
            this.list=[]
            this.feed(60)
        })
    },    
    beforeDestroy() {
        // bus.$off("change-set-photos");
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
            this.$store.dispatch("view",idx)
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
        menu(e,item,idx) {
            var menu = [];
            this.currentIndex=idx
            if(this.$store.state.selected.indexOf(item.path)<0)
                this.$store.dispatch('selectJustOne',item.path)

            if(this.$store.state.selected.length>0) {
                var all=true;
                for(var p of this.$store.state.selected)
                    all=all & (this.$store.getters.basket.indexOf(p)>=0)
                if(all)
                    menu.push(    {name:'Remove from basket', callback: ()=>{this.$store.dispatch('photoBasket',{path:null,bool:false})}  } )
                else
                    menu.push(    {name:'Add to basket', callback: ()=>{this.$store.dispatch('photoBasket',{path:null,bool:true})}  } )
                
                var tagsCanBeRemoved=new Set([]);
                var currentComment=null;
                this.$store.state.files.forEach(p=>{
                    if(this.$store.state.selected.indexOf(p.path)>=0) {
                        if(p.tags)
                            for(var tag of p.tags)
                                tagsCanBeRemoved.add(tag)
                        if(p.comment) {
                            if(currentComment==null)
                                currentComment=p.comment;
                            else
                                currentComment=""; //more than one -> no currentComment !
                        }
                    }
                })
            }
            if(this.$store.state.selected.length==1) {
                menu.push(    {name:'Select this album', callback: ()=>{this.$store.dispatch('selectPhoto',item.path)}});
                menu.push(    {name:'Select this time', callback: ()=>{this.$store.dispatch('selectTime',item.date)} } )
            }
            if(this.$store.state.selected.length>0) {
                menu.push(    {name:'> rotate left (Ctrl-L)', callback: ()=>{this.$store.dispatch('photoRotateLeft')} } )
                menu.push(    {name:'> rotate right (Ctrl-R)', callback: ()=>{this.$store.dispatch('photoRotateRight')} } )
                menu.push(    {name:'> change date', callback: notImplemented } )
                menu.push(    {name:'> rebuild thumbnail (Ctrl-T)', callback: ()=>{this.$store.dispatch('photoRebuildThumbnail')} } )
                menu.push(    {name:'> comment', callback: ()=>{
                    var txt=prompt("Comment ?",currentComment)
                    if(txt!=null)
                        this.$store.dispatch('photoComment',{path:null,txt: txt || ""})
                }})
                for(var tag of tagsCanBeRemoved)
                    menu.push(    {name:'Remove tag:'+tag, callback: (n)=>{
                        var tag=n.split(":")[1]
                        this.$store.dispatch('photoDelTag',tag)
                    }} )
                if(tagsCanBeRemoved.size>0) menu.push(    {name:'Remove all tags', callback: ()=>{this.$store.dispatch('photoClearTags')}} )
                menu.push(    {name:'Delete', callback: notImplemented } )
            }
            if(menu.length>0)
                this.$root.$refs.menu.pop(menu,e)
        },
    },
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
        justify-content: flex-start;
    }
    :scope > * {
        flex: 0 0 auto;
        height:180px;
    }

</style>
<style>
.click {cursor:pointer}
</style>
