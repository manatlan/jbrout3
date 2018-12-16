<template>
    <div>

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
        menu(e,path) {
            this.selectedPath = path;
            var menu = [
                {name:'Select only', callback: ()=>{this.$store.dispatch('selectAlbum',{path:this.selectedPath,all:false}) }},
                {name:'Rename', callback: notImplemented },
                {name:'New album', callback: notImplemented },
                {name:'Refresh', callback: ()=>{this.$store.dispatch('refreshAlbum',this.selectedPath)}  },
                {name:'Remove from jbrout', callback: notImplemented },
                {name:'Delete from disk', callback: notImplemented },

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
