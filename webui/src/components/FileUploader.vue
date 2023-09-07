<template>
    <div>
        <h1>Загрузка файла</h1>
        <form @submit.prevent="submitForm">
            <input type="file" ref="fileInput" @change="handleFileChange" :disabled="isProcessing" />
            <button type="submit" :disabled="isProcessing">
                {{ isProcessing ? 'Загрузка...' : 'Загрузить' }}
            </button>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const fileInput = ref<HTMLInputElement | null>(null);
const selectedFile = ref<File | null>(null);
const isProcessing = ref(false);

const handleFileChange = () => {
    if (fileInput.value && fileInput.value.files) {
        selectedFile.value = fileInput.value.files[0];
    }
};

const submitForm = async () => {
    if (!selectedFile.value) {
        alert('Please select a file.');
        return;
    }

    isProcessing.value = true; // Block the submit button and set processing text

    const formData = new FormData();
    formData.append('audio_file', selectedFile.value);
    formData.append('type', selectedFile.value.type);

    try {
        const base = 'http://localhost:9000';
        const lang = 'ru';
        const format = 'txt';
        const url = `${base}/asr?task=transcribe&language=${lang}&encode=true&output=${format}`;
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            // Handle the response content here, e.g., download the file
            const content = await response.json();
            if (content) {
                // Example: Create a text file download link
                const blob = new Blob([content.result], { type: 'text/plain' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = content.filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            }

            // Clear the file input
            fileInput.value!.value = '';

            // Reset processing state with a delay (to allow the button click event to finish)
            setTimeout(() => {
                isProcessing.value = false;
            }, 0);
        } else {
            alert('Произошла ошибка при загрузке файла');
            isProcessing.value = false;
        }
    } catch (error) {
        console.error('Error:', error);
        isProcessing.value = false;
    }
};
</script>
