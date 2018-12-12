<template>
    <div>
        <div
            :class="classItem"
            @click="parent.select(value.path)"
            @contextmenu.prevent="parent.menu($event,value.path)"
            @dblclick="$store.dispatch('selectAlbum',{path:value.path,all:true})"
            @click.middle="parent.select(value.path);$store.dispatch('selectAlbum',{path:value.path,all:false})"
            ><img src="gfx/folder.png"/> {{value.path | basename}} ({{value.items}})</div>

        <tree-folders v-for="(i,idx) in value.folders" :key="idx" :value="i" :parent="parent"/>
    </div>
</template>
<script>
export default {
    props:["value","parent"],
    computed: {
        classItem: function() {
            return (this.parent.selectedPath == this.value.path?'tselected':'')+" click";
        }
    }
}
</script>
<style scoped>
:scope {
    padding-left:10px;
}
.tselected {
    background: yellow;
}
</style>
