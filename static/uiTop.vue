<template>
    <div class="ui" @contextmenu.prevent="">

        <button @click="$store.dispatch('addFolder')"
            title="Add album in jBrout"
            >&#65291;</button>
        
        <span class="title">
            <span v-html="$store.state.content"></span><br/>
            <i v-if="$store.state.albumComment">{{$store.state.albumComment}}</i>
        </span>

        <div class="click basket"
            @click="selectBasket()" 
            v-if="$store.state.basket.length>0"
            @contextmenu.prevent="menubasket($event)"> <img src="gfx/basket.png"/> <span>{{$store.state.basket.length}}</span></div>
    </div>
</template>
<script>
export default {
    data() {
        return {};
    },
    methods: {
        selectBasket(path) {
            this.$store.dispatch('selectBasket')
        },
        menubasket(e) {
            var menu = [
                {name:'remove', callback: ()=>{this.$store.dispatch('removeBasket')} },
                {name:'export', callback: notImplemented },
            ];
            this.$root.$refs.menu.pop(menu,e)
        },        

    }
}
</script>
<style scoped>
    :scope {padding:10px}
    :scope .title{margin-left:230px;display: inline-block;}
    :scope .basket{float:right;}
    :scope .basket * {vertical-align: middle}
    .dropHighlight {background: white;}
</style>
