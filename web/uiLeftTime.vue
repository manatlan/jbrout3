<template>
    <div @contextmenu.prevent="">
        <div v-for="y in $store.state.years" :key="y.year">
            <expander :show="y.months.length>0" :value="y.expand" @click="expandYear(y)"></expander>
            <span class="click" :class="isSelected(y)" @click="select(y)" @dblclick="selectYear(y)">{{y.year}}</span>
            <div class="months click" :class="isSelected(m)" v-for="m in y.months" :key="m" v-show="y.expand" 
                @click="select(m)"
                @dblclick="$store.dispatch('getYearMonth',m)">
                {{m | monthname}}
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data:function() {
        return {selected:null}
    },  
    computed: {
    }  ,
    methods: {
        isSelected:function(y) {
            return y==this.selected?"selected":"";
        },
        selectYear:function (y) {
            this.$store.dispatch('getYear',y.year)
            y.expand=true
        },
        expandYear:function (y) {
            y.expand=!y.expand;
        },
        select:function(s) {
            this.selected=s;
        }
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
