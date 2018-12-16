<template>
    <div>
        <span class="click" @click="select(value)" @contextmenu.prevent="parent.menu($event,value)">
            <span :class="value.type">{{value.name}}</span>
             
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
            if(item.type=="tag")
                this.$store.dispatch('selectTags',[item.name])
            else {
                var gett=function(item) {
                    var tags=[]
                    for(var i of item.children) {
                        if(i.type=="tag")
                            tags.push(i.name)
                        else
                            tags=tags.concat( gett(i) )
                    }
                    return tags
                }
                this.$store.dispatch('selectTags',gett(item))
            }
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
