<template>
    <div @contextmenu.prevent="">
        Here will be the search-tab, to be able to search photos ;-)
        <div>
            <input type="date" :value="$store.state.datemin" :min="$store.state.datemin" :max="$store.state.datemax">min
        </div>
        <div>
            <input type="date" :value="$store.state.datemax" :min="$store.state.datemin" :max="$store.state.datemax">max
        </div>
    </div>
</template>
<style scoped>
    :scope {
        overflow-y:auto;
        background:white;
        padding:20px;
        color:#AAA;
    }
</style>
