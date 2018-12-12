<template>
    <div @contextmenu.prevent="menu">

        <thumb v-for="(i,idx) in $store.state.files" :key="idx"
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
        }
    },
    mounted() {
        this.$el.addEventListener('scroll', this.refreshDataSrc);
        this.$el.addEventListener('resize', this.refreshDataSrc);
    },
    methods: {
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
        refreshDataSrc(e) { //https://stackoverflow.com/questions/2321907/how-do-you-make-images-load-only-when-they-are-in-the-viewport
            console.log("refresh thumbs")
            var elements = document.querySelectorAll("img[data-src]");
            for (var i = 0; i < elements.length; i++) {
                    var boundingClientRect = elements[i].getBoundingClientRect();
                    if (elements[i].hasAttribute("data-src") && boundingClientRect.top < window.innerHeight) {
                        elements[i].setAttribute("src", elements[i].getAttribute("data-src"));
                        elements[i].removeAttribute("data-src");
                    }
            }
        },

    },
    watch: {
        '$store.state.files':function (to, from) {
            this.$el.scrollTop=0;
            Vue.nextTick( this.refreshDataSrc);
        },
        // drawer: function (to, from) {
        //     if(to==true) {
        //         document.activeElement.blur();
        //     }
        // }
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
