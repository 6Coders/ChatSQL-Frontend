<template>
  <div class="container d-flex flex-column vh-80" data-cy="request-page">
    <!-- Messaggi chat -->
    <div class="overflow-auto flex-grow-1 px-md-5 mb-5 chat-height" data-cy="chat">
      <ViewGeneratedPrompts :messages="requestStore.messages" :status="requestStore.isSending" />
    </div>

    <!-- Input per l'utente -->
    <div class="container input-group mt-2 px-md-5 pb-5 bg-white fixed-bottom" style="height: 100px;">
      <input type="text" class="form-control" v-model="requestStore.requestMessage" name="requestMessage"
        autocomplete="off" placeholder="Inserisci un prompt qui..." data-cy="request-input" @keyup.enter="submitForm" />
      <SendRequestButton :submitMethod="submitForm" :stopSubmitMethod="stopSending" :sendButtonClass="sendButtonClass"
        :stopSendButtonClass="stopSendButtonClass" :status="requestStore.isSending"
        :disabled="!requestStore.requestMessage" data-cy="send-request-button" />
      <button class="btn btn-secondary rounded mx-2" type="button" @click="clearMessages"
        v-if="requestStore.messages && requestStore.messages.length > 0" data-cy="clear-button">Cancella <i
          class="bi bi-trash"></i> </button>
      <div class="w-100 text-center mt-2">
        <small v-if="requestStore.selectedDictionary" data-cy="selected-dictionary" class="d-block">Dizionario dati
          caricato: <b>{{ requestStore.selectedDictionary
            }}</b></small>
        <small v-else data-cy="selected-dictionary" class="d-block"><b>Non è stato caricato alcun dizionario</b></small>
        <small class="d-block">Made by <a href="https://github.com/6Coders/ChatSQL">6Coders</a></small>
      </div>
    </div>
  </div>
</template>

<script>
import SendRequestButton from '@/components/SendRequestButton.vue'
import ViewGeneratedPrompts from '@/components/ViewGeneratedPrompts.vue'
import RequestPageViewModel from '@/viewmodel/VMRequest'
import { onMounted } from 'vue'

export default {
  name: 'RequestPage',
  components: {
    SendRequestButton,
    ViewGeneratedPrompts
  },
  setup() {
    const {
      requestStore, submitForm, stopSending, clearMessages, fetchSelectedDictionary
    } = RequestPageViewModel()

    onMounted(() => {
      fetchSelectedDictionary()
    })

    return {
      requestStore,
      submitForm,
      stopSending,
      clearMessages,
      /**
       * CSS class for the redirect button.
       * @type {String}
       */
      buttonClass: "btn btn-secondary rounded-0 rounded-end no-border-radius mr-2",

      /**
       * CSS class for the send button.
       * @type {String}
       */
      sendButtonClass: "btn btn-primary rounded-0 rounded-end no-border-radius mr-2",

      /**
       * CSS class for the stop send button.
       * @type {String}
       */
      stopSendButtonClass: "btn btn-warning rounded-0 rounded-end no-border-radius mr-2",

      /**
       * CSS class for the request input.
       * @type {String}
       */
      requestClass: "form-control no-border-radius"
    }
  }
}
</script>

<style scoped>
.chat-height {
  height: calc(100vh - 275px);
}

@media (min-width: 768px) {
  .no-border-radius {
    border-radius: 0;
  }

  .chat-height {
    height: calc(100vh - 200px);
  }
}
</style>