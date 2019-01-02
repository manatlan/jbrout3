<template>
    <div class='click' 
        @contextmenu.prevent="$emit('menu',$event)"
        @click="$emit('allclick',$event)" 
        @click.middle="$emit('allclick',$event)" 
        @dblclick="$emit('dblclick',$event)">
        <div class="photo">
            <img class="basket" src="gfx/basket.png" v-if="$store.getters.basket.indexOf(value.path)>=0"/>
            <img 
                @drop.prevent="drop" 
                @dragover="dragover" 
                
                draggable="true"
                @dragstart="dragstart" 
                @dragend="dragend" 
                :src="src" 
                :class="value.real=='no'?'thumb noexif':'thumb'"/>
        </div>

        <div class="text" v-if="$store.state.displayType=='name'">{{value.path | basename}}</div>
        <div class="text" v-if="$store.state.displayType=='tags'">{{value.tags && value.tags.join(", ")}}</div>
        <div class="text" v-if="$store.state.displayType=='date'">{{value.date | date}}</div>
        <div class="text" v-if="$store.state.displayType=='comment'">{{value.comment}}</div>
        <div class="text" v-if="$store.state.displayType=='album'">{{value.path | dirname}}</div>

    </div>
</template>
<script>
export default {
    props:["value","idx"],

    data:function() {
        return {reload:{}}
    },
    beforeMount() {
        bus.$on("change-photo",(path)=>{
            if(path==this.value.path)
                Vue.set(this.reload,path,new Date().getTime())
        })

        bus.$on("scroll-to-path",(path)=>{
            if(path==this.value.path)
                this.$el.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"})
        })
    },    
    beforeDestroy() {
        // bus.$off("change-photo")
        // bus.$off("scroll-to-path")
    },     
    computed: {
        src: function() {
            var ts=this.reload[this.value.path]
            if(ts)
                return '/thumb/'+this.value.path+'?idx='+this.idx+"&refresh="+ts;
            else
                return '/thumb/'+this.value.path+'?idx='+this.idx+"&refresh="+new Date().getTime();
        }
    },
    methods: {
        drop: function(ev) {
            var obj = JSON.parse( ev.dataTransfer.getData("text") );
            if(obj.tags) {
                if(this.$store.state.selected.indexOf(this.value.path)>=0) //multi
                    this.$store.dispatch("photoAddTags", {path:null,tags:obj.tags})
                else //single
                    this.$store.dispatch("photoAddTags", {path:this.value.path,tags:obj.tags})
            }
        },
        dragover: function(ev) {
            if(this.$store.state.dragging=="tag") // allow drop tag only
                ev.preventDefault();
        },
        dragstart: function(ev) {
            if(this.$store.state.selected.indexOf(this.value.path)<0)
                this.$store.dispatch('selectJustOne',this.value.path)

            ev.dataTransfer.setData("text",JSON.stringify({photos:"photos"}))
            this.$store.dispatch("dragging","photo")
        },        
        dragend: function(ev) {  
            this.$store.dispatch("dragging",null)
        },        
    },
}
</script>
<style scoped>
    :scope {
        height:auto;
        padding:5px;
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
