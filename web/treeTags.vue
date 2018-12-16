<template>
    <div>
        <span class="click" @click="select(value)" @contextmenu.prevent="parent.menu($event,value)">{{value.name}}</span>
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
            if(item.children.length==0)
                this.$store.dispatch('selectTags',[item.name])
            else {
                var gett=function(item) {
                    var tags=[]
                    for(var i of item.children) {
                        if(i.children.length==0)
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
.selected {
    background: yellow;
}
</style>
