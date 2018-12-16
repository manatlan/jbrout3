<template>
    <div class='click' 
        @contextmenu.prevent="$emit('menu',$event)"
        @click="$emit('allclick',$event)" 
        @click.middle="$emit('allclick',$event)" 
        @dblclick="$emit('dblclick',$event)">
        <div class="photo">
            <img class="basket" src="gfx/basket.png" v-if="$store.getters.basket.indexOf(value.path)>=0"/>
            <img class="thumb" :src="src" :class="value.real=='no'?'noexif':''"/>
        </div>
        

        <div class="text" v-if="$store.state.displayType=='name'">{{value.path | basename}}</div>
        <div class="text" v-if="$store.state.displayType=='tags'">{{value.tags && value.tags.join(", ")}}</div>
        <div class="text" v-if="$store.state.displayType=='date'">{{value.date}}</div>
        <div class="text" v-if="$store.state.displayType=='comment'">{{value.comment}}</div>
        <div class="text" v-if="$store.state.displayType=='album'">{{value.path | dirname}}</div>

    </div>
</template>
<script>
export default {
    props:["value","idx"],

    data:function() {
        return {refresh:false}
    },
    created() {
        bus.$on("change-photo",(path)=>{
            if(path==this.value.path)
                this.refresh=true;
        })
    },    
    computed: {
        src: function() {
            if(this.refresh) {
                this.refresh=false;
                return '/thumb/'+this.value.path+'?idx='+this.idx+"&refresh="+new Date().getTime();
            }
            else
                return '/thumb/'+this.value.path+'?idx='+this.idx;
        }
    },
    // mounted() {
    //     wuy.getInfo(this.idx,this.value.path)
    // }
}
</script>
<style scoped>
    :scope {
        height:auto;
        margin:2px;
        text-align:center;
    }
    div.photo {
        width:160px;
        height:160px;
        position: relative;
    }
    div.photo img.thumb {
        max-width: 100%;
        max-height: 100%;
        width: auto;
        height: auto;
    
        position: absolute;  
        top: 0;  
        bottom: 0;  
        left: 0;  
        right: 0;  
        margin: auto;
        
        border:4px solid white;
        box-shadow: 0 0 10px #888;

    }
    .noexif {
        border:4px solid red !important;
        box-shadow: 0 0 10px red !important;
    }
    div.text {
        text-align:center;   
        width:160px;
    }
    div.photo img.basket {
        position:relative;
        top:0px;
        z-index:2;
        left:-60px;
    }
</style>
