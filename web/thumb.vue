<template>
    <div class='click' @click="$emit('allclick',$event)" @click.middle="$emit('allclick',$event)" @dblclick="$emit('dblclick',$event)">
        <img :data-src="'/thumb/'+value.path"/>
        <div class="text" v-if="$store.state.displayType=='name'">{{value.path | basename}}</div>
        <div class="text" v-if="$store.state.displayType=='tags'">{{value.tags.join(", ")}}</div>
        <div class="text" v-if="$store.state.displayType=='date'">{{value.date}}</div>
        <div class="text" v-if="$store.state.displayType=='comment'">{{value.comment}}</div>
        <div class="text" v-if="$store.state.displayType=='album'">{{value.path | dirname}}</div>
    </div>
</template>
<script>
export default {
    props:["value"]
}
</script>
<style scoped>
    :scope {
        text-align: center;
    }
    img {
        width:120px;
        height:120px;
        display:inline-block
    }
    div.text {}
</style>
