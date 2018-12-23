<template>
    <vbox class="ui">
        <hbox class="bmin" @contextmenu.prevent="">
            <a href="#" @click="$store.dispatch('selectTab',1)" :class="getClass(1)">Albums</a>
            <a href="#" @click="$store.dispatch('selectTab',2)" :class="getClass(2)">Time</a>
            <a href="#" @click="$store.dispatch('selectTab',3)" :class="getClass(3)">Tags</a>
            <a href="#" @click="$store.dispatch('selectTab',4)" :class="getClass(4)">Search</a>
        </hbox>
        <hbox class="bmax" @contextmenu.prevent="">
            <uiLeftAlbums v-show="$store.state.tab==1" class="leftwidth"/>
            <uiLeftTime v-show="$store.state.tab==2" class="leftwidth"/>
            <uiLeftTags v-show="$store.state.tab==3" class="leftwidth"/>
            <uiLeftSearch v-show="$store.state.tab==4" class="leftwidth"/>
        </hbox>
    </vbox>
</template>
<script>
export default {
    props: ["value","show"],
    data: function() {
        return {
        }
    },
    mounted() {
    },    
    computed: {
    },
    methods: {
        getClass:function(n) {
            return n==this.$store.state.tab ? "selected" : "";
        }
    },
}
</script>
<style scoped>
    :scope {}
    a {padding:4px;text-decoration:none}
    .selected {background:white}

    .leftwidth {flex: 0 0 250px;width:250px}
</style>
