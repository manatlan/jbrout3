<template>
    <div class="ui" @contextmenu.prevent="">


        <button @click="$store.dispatch('addFolder')"
            @dragover.prevent="mydragover($event)"
            @dragleave.prevent="mydragend($event)"
            @dragend.prevent="mydragend($event)"
            @drop.prevent="mydrop(null,$event)"
            >+</button>

        <span style="float:right">
            <a href="#" @click="menuDisplay($event)" @contextmenu.prevent="menuDisplay($event)">display({{$store.state.displayType}})</a>
            <a href="#" @click="menuOrder($event)" @contextmenu.prevent="menuOrder($event)">order({{$store.state.orderReverse?"D":"A"}})</a>
        </span>
    </div>
</template>
<script>
export default {
    data() {
        return {};
    },
    methods: {
        menuDisplay(e) {
            var menu = [
                {name:'name', callback: (n)=>{this.$store.dispatch("setDisplayType",n)} },
                {name:'tags', callback: (n)=>{this.$store.dispatch("setDisplayType",n)} },
                {name:'date', callback: (n)=>{this.$store.dispatch("setDisplayType",n)} },
                {name:'comment', callback: (n)=>{this.$store.dispatch("setDisplayType",n)} },
                {name:'album', callback: (n)=>{this.$store.dispatch("setDisplayType",n)} },
            ];
            this.$root.$refs.menu.pop(menu,e)
        },
        menuOrder(e) {
            var menu = [
                {name:'ascending', callback:  (n)=>{this.$store.dispatch("setOrderReverse",false)} },
                {name:'descending', callback:  (n)=>{this.$store.dispatch("setOrderReverse",true)} },
            ];
            this.$root.$refs.menu.pop(menu,e)
        },

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
    }
}
</script>
<style scoped>
    :scope {padding:10px}
    a {text-decoration:none}
    .dropHighlight {background: white;}
</style>
