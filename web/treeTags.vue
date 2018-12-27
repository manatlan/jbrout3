<template>
    <div>
        <expander :show="value.type=='cat' && value.children.length>0" @click="expand" :value="value.expand"></expander>
        <span class="click" @click="select(value.name)" @dblclick="search(value)" @contextmenu.prevent="parent.menu($event,value)">
            <span :class="value.type +' '+ isSelected(value.name)"
                @dragstart="dragstart" 
                @dragend="dragend" 
                draggable="true"

                @drop.prevent="drop" 
                @dragover="dragover"                 
                >{{value.name}}</span>
             
        </span>
        <tree-Tags v-for="(i,idx) in value.children" :key="idx" :value="i" :parent="parent" v-show="value.expand==true"/>
    </div>
</template>
<script>
export default {
    props:["value","parent"],
    computed: {
    },
    methods: {
        select:function(n) {
            this.parent.selectedTag=n;
        },
        isSelected:function(n) {
            return this.parent && n==this.parent.selectedTag?"selected":"";
        },
        expand:function(v) {
            this.$store.dispatch('catExpand',{name:this.value.name,bool:v})
            this.value.expand=v; // NOT TOP (change state outside of mystore !!!!)
        },        
        search(item) {
            this.$store.dispatch('selectTags',{tags:this._getTags(item),cat: item.type=="cat"?item.name:null})
        },
        dragstart: function(ev) {        
            this.$store.dispatch("dragging","tag")
            ev.dataTransfer.setData("text",JSON.stringify( {tags:this._getTags(this.value),name:this.value.name,type:this.value.type} ))
        },
        dragend: function(ev) {        
            this.$store.dispatch("dragging",null)
        },
        _getTags(item) {    // duplicated in uiLeftTags.vue ;-(
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
        drop: function(ev) {
            var obj = JSON.parse( ev.dataTransfer.getData("text") );
            if(obj.type=="cat") this.$store.dispatch('catMoveToCat',{cat1:obj.name,cat2:this.value.name})
            if(obj.type=="tag") this.$store.dispatch('tagMoveToCat',{tag:obj.name,cat:this.value.name})

        },
        dragover: function(ev) {
            if(this.$store.state.dragging=="tag") // allow drop tag only
                ev.preventDefault();        },
    }
}
</script>
<style scoped>
:scope {
    padding-left:10px;
}
:scope *{
    vertical-align: middle;
}
:scope span.tag{
}
:scope span.cat{
    color: #AAA;
}
:scope span.cat:before {
    content: "[";
}
:scope span.cat:after {
    content: "]";
}

.selected {
    background: yellow;
}

</style>
