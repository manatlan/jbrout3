<template>
    <div>

        <tree-tags v-for="(i,idx) in $store.state.tags" :key="idx" :value="i"/>

    </div>
</template>
<style scoped>
    :scope {
        overflow-y:auto;
        background:white;
    }
</style>
