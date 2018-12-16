<template>
    <div @contextmenu.prevent="">
        <div v-for="year in $store.state.years"
            class="click"
            @click="$store.dispatch('getYear',year)">{{year}}</div>

        <i>!!! NOT FINISHED !!!</i>
    </div>
</template>
<style scoped>
    :scope {
        overflow-y:auto;
        background:white;
        padding:5px;
    }
    :scope div {margin:4px;}
</style>
