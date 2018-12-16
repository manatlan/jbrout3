<template>
    <vbox class="ui">
        <hbox class="bmin" @contextmenu.prevent="">
            <a href="#" @click="setTab(1)" :class="getClass(1)" >Albums</a>
            <a href="#" @click="setTab(2)" :class="getClass(2)">Time</a>
            <a href="#" @click="setTab(3)" :class="getClass(3)">Tags</a>
            <a href="#" @click="setTab(4)" :class="getClass(4)">Search</a>
        </hbox>
        <hbox class="bmax" @contextmenu.prevent="">
            <uiLeftAlbums v-show="tab==1" class="leftwidth"/>
            <uiLeftTime v-show="tab==2" class="leftwidth"/>
            <uiLeftTags v-show="tab==3" class="leftwidth"/>
            <uiLeftSearch v-show="tab==4" class="leftwidth"/>
        </hbox>
    </vbox>
</template>
<script lang="python" type="text/python">
class Component:
    def __init__(self):
        self.tab=1
    def setTab(self,n):
        self.tab=n
        if n==2: self["$store"].dispatch("getYears")
    def getClass(self,n):
        return n==self.tab and "selected" or ""

</script>
<style scoped>
    :scope {}
    a {padding:4px;text-decoration:none}
    .selected {background:white}

    .leftwidth {flex: 0 0 250px;width:250px}
</style>
