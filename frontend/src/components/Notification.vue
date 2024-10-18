<template>
    <div v-if="visible" class="notification">
    <div class="alert alert-success">
      {{ message }}
    </div>
  </div>
</template>


<script>
export default {
  name: "SuccessNotification",
  props: {
    message: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      visible: false
    };
  },
  methods: {
    show() {
      this.visible = true;
      setTimeout(() => {
        this.visible = false;
      }, 3000);
    }
  }
};
</script>

<style scoped>
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  width: 300px;
}
</style>