<template>
    <div @contextmenu.prevent="">

        <tree-tags v-for="(i,idx) in $store.state.tags" :key="idx" :value="i" :parent="current"/>

    </div>
</template>
<script>
export default {
    data: function() {
        return {
            current: this,
            selectedTag:null,
        }
    },
    created() {
    },        
    methods: {
        menu(e,item) {
            console.log(item)
            var menu = [];
            if(item.type=="cat") menu.push( {name:'Add a tag', callback: ()=>{this.$store.dispatch("tagsAddTag", item.name)} } )
            if(item.type=="cat") menu.push( {name:'Add a category', callback:  ()=>{this.$store.dispatch("tagsAddCat", item.name)} } );
            if(item.name!="Tags") {
                if(item.type=="cat") menu.push( {name:'Rename category', callback:  ()=>{this.$store.dispatch("catRename", item.name)} } );
                if(item.type=="cat")
                    menu.push( {name:'Delete', callback: ()=>{this.$store.dispatch("tagsDelCat", {cat:item.name,tags:this._getTags(item)}) }} );
                else
                    menu.push( {name:'Delete', callback: ()=>{this.$store.dispatch("tagsDelTag", item.name)} } );
            }
            this.$root.$refs.menu.pop(menu,e)
        },  
        _getTags(item) {    // duplicated in treeTags.vue ;-(
            var tags=[]
            if(item.type=="tag")
                tags.push(item.name)
            for(var i of item.children) {
                if(i.type=="tag")
                    tags.push(i.name)
                else
                    tags=tags.concat( this._getTags(i) )
            }
            return tags
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
