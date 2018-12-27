<template>
    <div @contextmenu.prevent="">
        <div v-for="y in $store.state.years" :key="y.year">
            <expander :show="y.months.length>0" :value="y.expand" @click="expandYear(y)"></expander>
            <span class="click" @dblclick="expandYear(y)">{{y.year}}</span>
            <div class="months click" v-for="m in y.months" :key="m" v-show="y.expand" @dblclick="$store.dispatch('getYearMonth',m)">
                {{m | monthname}}
            </div>
        </div>
    </div>
</template>
<script>
export default {
    methods: {
        expandYear:function (y) {
            if(y.expand==false) {
                this.$store.dispatch('getYear',y.year)
            }
            y.expand=!y.expand;
        },
    },
}
</script>
<style scoped>
    :scope {
        overflow-y:auto;
        background:white;
        padding:5px;
    }
    :scope *{
        vertical-align: middle;
    }
    :scope div {margin:4px;}
    :scope div.months {padding-left:30px;}
</style>
