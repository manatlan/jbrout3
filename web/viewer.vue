<template>
    <div v-if="$store.getters.photo!=null"
        @click="hide()"
        @contextmenu.prevent="hide()"
        @wheel="$store.dispatch('view',$event.deltaY>0?'next':'previous')"
        @click.right="hide()"
        @click.middle="hide()"
        :style='src'>

        <div>{{$store.state.viewerIdx+1}}/{{$store.state.files.length}}</div>
        <div>Name: {{$store.getters.photo.path | basename}}</div>
        <div>Tags: {{tags}}</div>
        <div>Comment: {{comment}}</div>
        <div>Resolution: {{resolution}}</div>
        <div>Album: {{$store.getters.photo.path | dirname}}</div>
        <div>Date: {{$store.getters.photo.date | date}}</div>
    </div>
</template>
<script>
export default {
    data: function() {
        return {
            reload:{},
        }
    },
    created() {
        bus.$on("change-photo",(path)=>{
            Vue.set(this.reload,path,new Date().getTime())
        })
    },    
    computed: {
        src: function() {
            if(this.$store.getters.photo!=null) {
                var ts=this.reload[this.$store.getters.photo.path]
                if(ts)
                    return `background-image: url("/image/`+this.$store.getters.photo.path+`?idx=`+this.$store.state.viewerIdx+"&refresh="+ts+`")`
                else
                    return `background-image: url("/image/`+this.$store.getters.photo.path+`?idx=`+this.$store.state.viewerIdx+`")`
            }
        },
        resolution: function() {
            if(this.$store.getters.photo!=null) {
                return this.$store.getters.photo.resolution
            }
        },
        tags: function() {
            if(this.$store.getters.photo!=null) {
                return this.$store.getters.photo.tags.join(", ")
            }
        },
        comment: function() {
            if(this.$store.getters.photo!=null) {
                return this.$store.getters.photo.comment
            }
        }
    },

    methods: {
        hide() {
            this.$store.dispatch("view",null)
        },
    },
}
</script>
<style scoped>
:scope {
    position:fixed;
    left:0px;
    right:0px;
    top:0px;
    bottom:0px;
    z-index:2;
    color:white;
    width:100%;height:100%;
    background-size:contain;
    background-position: center;
    background-color:black;
    background-repeat:no-repeat;
}
</style>

