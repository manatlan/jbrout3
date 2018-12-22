<template>
    <div>
        <div
            :class="classItem"
            @click="parent.select(value.path)"
            @contextmenu.prevent="parent.menu($event,value.path)"
            @dblclick="$store.dispatch('selectAlbum',{path:value.path,all:true})"
            @click.middle="parent.select(value.path);$store.dispatch('selectAlbum',{path:value.path,all:false})"

            @drop.prevent="drop" 
            @dragover.prevent="dragover"     

            draggable="true"
            @dragstart="dragstart" 
            @dragend="dragend"                     
            ><img src="gfx/folder.png"/> {{value.path | basename}} 
            <span v-show="value.items">({{value.items}})</span>
        </div>

        <tree-folders v-for="(i,idx) in value.folders" :key="idx" :value="i" :parent="parent"/>
    </div>
</template>
<script>
export default {
    props:["value","parent"],
    computed: {
        classItem: function() {
            return "item "+ (this.parent.selectedPath == this.value.path?'tselected':'')+" click " + (this.value.items>0?"":"nophotos");
        }
    },
    methods: {
        drop: function(ev) {
            var obj = JSON.parse(ev.dataTransfer.getData("text"));
            if(obj.photos)
                this.$store.dispatch('photoMoveAlbum',this.value.path)
            if(obj.album)
                this.$store.dispatch('albumMoveAlbum',{path1:obj.album,path2:this.value.path})
        },
        dragover: function(ev) {
        },      
        
        dragstart: function(ev) {
            ev.dataTransfer.setData("text",JSON.stringify({album:this.value.path}))
            this.$store.dispatch("dragging","album")
        },        
        dragend: function(ev) {  
            this.$store.dispatch("dragging",null)
        },          
    }
}
</script>
<style scoped>
:scope {
    padding-left:10px;
}
:scope div.item *{
    vertical-align: middle;
}

.tselected {
    background: yellow;
}
.nophotos {
    color: #AAA;
}
</style>
