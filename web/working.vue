<template>
    <div v-show="$store.state.working!=null" contextmenu.prevent="">
        <div id="txt">{{$store.state.working}}</div>
    </div>
</template>
<script>
export default {
    data: function() {
        return {
        }
    },
    created() {
    },
    computed: {
    },

    methods: {
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
    z-index:10;
    background: #000;
    opacity: 0.4;
    width:100%;height:100%;

            display:flex;
            flex-flow: row no-wrap;
            justify-content: center;
            align-items: center;
}
:scope #txt {
            flex: 1 1 auto;
            text-align: center;
            /*vertical-align:middle;*/
            text-shadow: 0 0 0.5em black, 0 0 0.2em white;
            color: white;
            font-size: 20px;
            text-decoration:none;
            opacity: 1;
        }
</style>

