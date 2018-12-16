<template>
    <ul tabindex="-1" ref="popmenu" v-if="menus.length>0" @blur="menus=[]" class="noselect" :style="style" @contextmenu.prevent="">
        <li v-for="i in menus" @click="caller(i)">{{i.name}}</li>
    </ul>
</template>
<script>
export default { // INDEPENDANT (REUSABLE)
    data: function() {
        return {
            menus:[],
            style: { top: '0px',left: '0px'},
        }
    },

    methods: {
        caller(item) {
            this.menus=[];
            this.$forceUpdate();
            setTimeout(function() {
                item.callback(item.name);
            }.bind(this),2);

        },

        pop: function( items, e) {
            this.menus=items

            Vue.nextTick(function() {
                this.$refs.popmenu.focus();
                var top=e.clientY, left=e.clientX;
                var maxHeight = window.innerHeight - this.$refs.popmenu.offsetHeight - 25;
                var maxWidth = window.innerWidth - this.$refs.popmenu.offsetWidth - 25;

                this.style.top = (top > maxHeight?maxHeight:top) + 'px';
                this.style.left = (left > maxWidth?maxWidth:left) + 'px';
            }.bind(this));
        }
    }
}
</script>
<style scoped>
:scope {
    background: ButtonFace;
    box-shadow: 0 2px 2px 0 rgba(0,0,0,.64);
    display: block;
    list-style: none;
    margin: 0;
    padding: 0;
    position: absolute;
    width: 200px;
    z-index: 999999;
}

:scope li {
    border-bottom: 1px solid #E0E0E0;
    color:black;
    margin: 0;
    padding: 5px 20px;
    cursor:pointer;
}

:scope li:last-child {
    border-bottom: none;
}

:scope li:hover {
    background: #1E88E5;
    color: #FAFAFA;
}
</style>
