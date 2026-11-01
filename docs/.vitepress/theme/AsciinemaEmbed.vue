<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import { useData } from "vitepress";
import "asciinema-player/dist/bundle/asciinema-player.css";

const props = defineProps({
  mobileOnly: Boolean,
  desktopOnly: Boolean,
});

const container = ref(null);
const isVisible = ref(false);
const { theme } = useData();
let playTimer;
let player;

onMounted(async () => {
  const isMobile = window.matchMedia("(max-width: 640px)").matches;

  if ((props.mobileOnly && !isMobile) || (props.desktopOnly && isMobile)) {
    return;
  }

  const AsciinemaPlayer = await import("asciinema-player");
  const { src, loop, preload, playDelay } = theme.value.asciinema;
  player = AsciinemaPlayer.create(src, container.value, {
    autoplay: false,
    loop,
    preload,
  });
  isVisible.value = true;
  playTimer = window.setTimeout(() => {
    void player?.play();
  }, playDelay);
});

onBeforeUnmount(() => {
  window.clearTimeout(playTimer);
  player?.dispose();
});
</script>

<template>
  <div
    ref="container"
    class="asciinema-embed"
    :class="{
      'is-visible': isVisible,
      'asciinema-embed--mobile': mobileOnly,
      'asciinema-embed--desktop': desktopOnly,
    }"
  />
</template>
