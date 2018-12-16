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
            if(item.type=="cat") menu.push( {name:'Rename category', callback: notImplemented } );
            if(item.type=="cat")
                menu.push( {name:'Delete', callback: ()=>{this.$store.dispatch("tagsDelCat", item.name)} } );
            else
                menu.push( {name:'Delete', callback: ()=>{this.$store.dispatch("tagsDelTag", item.name)} } );
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
