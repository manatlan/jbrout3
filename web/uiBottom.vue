<template>
    <div class="ui" @contextmenu.prevent="">
        <span style="float:right">
            {{$store.state.selected.length}}/
            {{$store.state.files.length}}
        </span>
    </div>
</template>
<script>
export default {
    data() {
        return {cpt:0};
    },
    methods: {
        inc() { this.cpt+=1; }
    }
}
</script>
<style scoped>
    :scope {}
</style>
