<template>
    <vbox>
        <ui-top class="bmin"/>
        <hbox class="bmax">
            <ui-left class="bmin"/>
            <ui-main class="bmax"/>
        </hbox>
        <ui-bottom class="bmin"/>
    </vbox>
</template>
<script>
export default {
    mounted() {
        this.$store.dispatch("init")
    },
}
</script>
<style scoped>
    :scope {
        width:100%;
        height:100%;
        display:flex;
        overflow:hidden;
    }

</style>
