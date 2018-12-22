<template>
    <div v-if="$store.state.notify.length>0" contextmenu.prevent="">
        {{$store.state.notify[0]}}
    </div>
</template>
<script>
export default {
    data: function() {
        return {
        }
    },
    mounted() {
    },    
    computed: {
    },
    methods: {
    },
}
</script>
<style scoped>
:scope {
    position:fixed !important;
    right:10px;
    bottom:10px;
    max-width:33%;
    z-index:10000000;
    color:white;
    padding:10px;
    background:black;
    box-shadow: 0 0 10px #888;
    border-radius:8px;
}
</style>

