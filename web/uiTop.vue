<template>
    <div class="ui" @contextmenu.prevent="">


        <button @click="$store.dispatch('addFolder')"
            @dragover.prevent="mydragover($event)"
            @dragleave.prevent="mydragend($event)"
            @dragend.prevent="mydragend($event)"
            @drop.prevent="mydrop(null,$event)"
            >+</button>
        <span class="title" v-html="$store.state.content"></span>

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
        mydragover(e) { e.target.classList.add("dropHighlight") },
        mydragend(e) { e.target.classList.remove("dropHighlight") },
        mydrop(i,e) {
            e.target.classList.remove("dropHighlight")
//~             for(var item of e.dataTransfer.items)
//~                 console.log("===",item.getAsFile().path)

            var items  = e.dataTransfer.items;      // -- Items
            for (var i = 0; i < items.length; i++)
            {
                var entry = items[i].webkitGetAsEntry();
                var file = items[i].getAsFile();
                console.log("===",items[i],entry,file)
            }
        },

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
    :scope .title{margin:230px}
    :scope .basket{float:right;}
    :scope .basket * {vertical-align: middle}
    .dropHighlight {background: white;}
</style>
