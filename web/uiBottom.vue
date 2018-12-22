<template>
    <div class="ui" @contextmenu.prevent="">
        <span style="float:right">
            {{$store.state.selected.length}}
            /
            {{$store.state.files.length}}
        </span>
        <span style="float:right">
            <a class="space" href="#" @click="menuDisplay($event)" @contextmenu.prevent="menuDisplay($event)">display : <b>{{$store.state.displayType}}</b></a>
            <a class="space" href="#" @click="menuOrder($event)" @contextmenu.prevent="menuOrder($event)">order : {{$store.state.orderReverse?"&#9660;":"&#9650;"}}</a>
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
                {name:'&#9650; ascending', callback:  (n)=>{this.$store.dispatch("setOrderReverse",false)} },
                {name:'&#9660; descending', callback:  (n)=>{this.$store.dispatch("setOrderReverse",true)} },
            ];
            this.$root.$refs.menu.pop(menu,e)
        },
    }
}
</script>
<style scoped>
    :scope .space {margin-right:30px;}
</style>
