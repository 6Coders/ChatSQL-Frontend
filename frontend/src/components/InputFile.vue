<template>
  <div>
    <div class="input-group">
      <input type="file" class="form-control" ref="fileInput" @change="handleFileUpload" data-cy="file-input" />
      <upload-button ref="uploadbtn" :class="uploadButtonClass" @upload-click="emitFile" :disabled="!file"
        :isuploading="isUploading" data-cy="upload-button" />
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import UploadButton from '@/components/UploadButton.vue';

export default {
  name: 'InputFile',
  components: {
    UploadButton
  },
  /**
   * Component for handling file input.
   *
   * @props {String} uploadButtonClass - The CSS class for the upload button.
   */
  props: {
    uploadButtonClass: String
  },
  setup(props, { emit }) {

    /**
     * @property {ref} file - A reference to the selected file.
     * @property {ref} message - A reference to the message associated with the file.
     * @property {ref} isUploading - A reference to a boolean indicating if the file is currently being uploaded.
     */
    const file = ref(null);
    const isUploading = ref(false);

    /**
     * Handles the file upload event.
     * Clears the message and assigns the selected file to the 'file' variable.
     *
     * @param {Event} event - The file upload event.
     */
    function handleFileUpload(event) {
      file.value = event.target.files[0];
    }

    /**
     * Emits the selected file.
     * 
     * @function emitFile
     * @emits file-selected - Event emitted when a file is selected
     */
    function emitFile() {
      if (file.value) {
        isUploading.value = true;
        emit('file-selected', file.value);
      }
    }

    /**
     * Sets the value of the isUploading reactive variable.
     *
     * @param {boolean} value - The new value for isUploading.
     */
    function setIsUploading(value) {
      isUploading.value = value;
    }

    return {
      file,
      handleFileUpload,
      emitFile,
      isUploading,
      setIsUploading
    };
  }
};
</script>
