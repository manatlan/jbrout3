<template>
    <div>
        <span class="click" @dblclick="select(value)" @contextmenu.prevent="parent.menu($event,value)">
            <span :class="value.type"
                @dragstart="dragstart" 
                draggable="true"

                @drop.prevent="drop" 
                @dragover="dragover"                 
                >{{value.name}}
            </span>
             
        </span>
        <tree-Tags v-for="(i,idx) in value.children" :key="idx" :value="i" :parent="parent"/>
    </div>
</template>
<script>
export default {
    props:["value","parent"],
    computed: {
    },
    methods: {
        select(item) {
            this.$store.dispatch('selectTags',this._getTags(item))
        },
        dragstart: function(ev) {        
            ev.dataTransfer.setData("text",JSON.stringify( {tags:this._getTags(this.value),name:this.value.name,type:this.value.type} ))
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
            if( this.value.type=="cat" )
                ev.preventDefault()
        },
    }
}
</script>
<style scoped>
:scope {
    padding-left:10px;
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
