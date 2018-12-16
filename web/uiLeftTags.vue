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
            if(item.type=="cat") menu.push( {name:'Add a tag', callback: notImplemented } )
            if(item.type=="cat") menu.push( {name:'Add a category', callback: notImplemented } );
            if(item.type=="cat") menu.push( {name:'Rename category', callback: notImplemented } );
            menu.push( {name:'Delete', callback: notImplemented } );
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
