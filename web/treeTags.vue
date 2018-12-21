<template>
    <div>
        <span class="click" @dblclick="select(value)" @contextmenu.prevent="parent.menu($event,value)">
            <span :class="value.type"
                @dragstart="dragstart" 
                draggable="true"
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
            ev.dataTransfer.setData("text",JSON.stringify(this._getTags(this.value)))
        },
        _getTags(item) {
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
        }        
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
