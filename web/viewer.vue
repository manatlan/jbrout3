<template>
    <div v-if="idx!=null"
        @click="hide()"
        @contextmenu.prevent="hide()"
        @wheel="scroll($event.deltaY)"
        @click.right="hide()"
        @click.middle="hide()"
        @keyup="test($event)"

        :style='src'>
        <div>{{idx+1}}/{{$store.state.files.length}}</div>
        <div>Tags: {{item.tags && item.tags.join(", ")}}</div>
        <div>Comment: {{item.comment}}</div>
        <div>Album: {{item.path | dirname}}</div>
        <div>Resolution: {{item.resolution}}</div>
        <div>Date: {{item.date}}</div>
    </div>
</template>
<script>
export default {
    data: function() {
        return {
            idx:null,
            item:{path:"",tags:[],comment:"",resolution:"",date:""},
            reload:{},
        }
    },
    created() {
        bus.$on("change-photo",(path)=>{
            this.reload[path]=new Date().getTime();
        })
    },    
    computed: {
        src: function() {
            if(this.item.path in this.reload) {
                return `background-image: url("/image/`+this.item.path+`?idx=`+this.idx+"&refresh="+this.reload[this.item.path]+`")`
            }
            else
                return `background-image: url("/image/`+this.item.path+`?idx=`+this.idx+`")`
        }
    },

    methods: {
        test(e) {
            console.log(e)
            alert(42)
        },
        view(idx) {
            this.idx=idx;
            this.item=this.$store.state.files[this.idx];
        },
        scroll(sens) {
            if(sens>0)
                this.idx+=1
            else
                this.idx+=-1

            this.idx=(this.$store.state.files.length+this.idx)%this.$store.state.files.length;
            this.item=this.$store.state.files[this.idx];
        },
        hide() {
            this.idx=null;
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

