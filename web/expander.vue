<template>
    <span>
        <span v-if="show">
            <span class="click" v-show="value" @click="$emit('click',false)">&#9660;</span>
            <span class="click" v-show="!value" @click="$emit('click',true)">&#9654;</span>
        </span>
    </span>
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
    },
}
</script>
<style scoped>
:scope {
    display:inline-block;
    width:17px;
    height:17px;
    overflow:hidden;
}
</style>

