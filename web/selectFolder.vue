<template>
        <vbox v-if="path">
            <div class="bmin">
                <button @click="end">X</button>{{title}}
            </div>
            <div class="bmax selecter">
                <div v-for="i in list">
                    <span v-if="i.isdir" @click="browse(i.path)" class="click">&#128447; {{i.name}}</span>
                    <span v-else>{{i.name}}</span>
                </div>

            </div>
            <hbox class="bmin">
                <input v-model="path" @change="changeManually" class="bmax"/>
                <button class="bmin" @click="select">OK</button>

            </hbox>
        </vbox>
</template>
<script>
export default {
    data: function() {
        return {
            title:"",
            callback:null,
            list:[],
            path:null,
            precpath:null,
        }
    },
    mounted() {
        bus.$on("choose-folder", ( title, origin, callback )=> {
            this.title=title;
            this.callback=callback;
            this.browse(origin);
        })
    },
    methods: {
        end:function() {
            this.path=null;
        },
        browse:function(path) {
            this.path=path;
            this.precpath=path;
            wuy.dir(path).then( ll=>{
                this.list=ll;
                log(ll)
                this.$forceUpdate()
            })
        },
        changeManually:function(e) {
            wuy.dir(this.path).then( ll=>{
                this.browse(this.path)
            }).catch( err=>{
                this.path=this.precpath
            })
        },
        select:function() {
            this.callback( this.path )
            this.end();
        },
    }
}
</script>
<style scoped>
:scope {
    padding:10px;
    position:fixed;
    left:0px;
    right:0px;
    top:0px;
    bottom:0px;
    z-index:100;
    background: buttonface;
    width:100%;height:100%;
}
.selecter {
    display:flex;
    flex-flow: column wrap;
    overflow:auto;
    background:white;
}
</style>
