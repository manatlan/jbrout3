<template>
    <div @contextmenu.prevent="">

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
    beforeMount() {
        bus.$on("select-path",(path)=>{
            this.select(path)
        })
    },    
    beforeDestroy() {
        bus.$off("select-path")
    },               
    methods: {
        select(path) {
            this.selectedPath = path;

            var expandPath=function(f) {
                for(var o of f) {
                    if(path.startsWith(o.path+"/")) o.expand=true;
                    expandPath(o.folders)
                }
            }
            expandPath(this.$store.state.folders)
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
    }
}
</script>
<style scoped>
    :scope {
        overflow-y:auto;
        background:white;
    }
</style>
