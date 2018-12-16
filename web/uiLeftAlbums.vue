<template>
    <div>
        <div class="click" style="padding-left:10px;"
            @click="selectBasket()" 
            v-if="$store.state.basket.length>0"
            @contextmenu.prevent="menubasket($event)"> <img src="gfx/basket.png"/>basket ({{$store.state.basket.length}})</div>
        <tree-folders v-for="(i,idx) in $store.state.folders" :key="idx" :value="i" :parent="current"/>

    </div>
</template>
<script>
export default {
    data: function() {
        return {
            selectedPath: null,
            current: this,
        }
    },
    methods: {
        select(path) {
            this.selectedPath = path;
        },
        selectBasket(path) {
            this.$store.dispatch('selectBasket')
        },
        menu(e,path) {
            this.selectedPath = path;
            var menu = [
                {name:'Select only', callback: ()=>{this.$store.dispatch('selectAlbum',{path:this.selectedPath,all:false}) }},
                {name:'Rename', callback: notImplemented },
                {name:'New album', callback: notImplemented },
                {name:'Refresh', callback: ()=>{this.$store.dispatch('refreshAlbum',this.selectedPath)}  },
                {name:'Remove from jbrout', callback: ()=>{this.$store.dispatch('removeAlbum',this.selectedPath)}},
                {name:'Delete from disk', callback: notImplemented },

            ];
            this.$root.$refs.menu.pop(menu,e)
        },
        menubasket(e) {
            var menu = [
                {name:'remove', callback: ()=>{this.$store.dispatch('removeBasket')} },
            ];
            this.$root.$refs.menu.pop(menu,e)
        },        
    }
}
</script>
<style scoped>
    :scope {
        overflow-y:auto;
        background:white;
    }
</style>
