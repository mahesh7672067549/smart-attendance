let cameraReady = false;

function ensureStatusBox() {
  if (document.getElementById('cameraStatus')) return;
  const statusBox = document.createElement('div');
  statusBox.id = 'cameraStatus';
  statusBox.className = 'message';
  const container = document.querySelector('.container');
  if (container) container.appendChild(statusBox);
}

function setCameraStatus(message, isError = false) {
  ensureStatusBox();
  const statusEl = document.getElementById('cameraStatus');
  if (!statusEl) return;
  statusEl.textContent = message;
  statusEl.className = isError ? 'message error' : 'message';
}

function startCamera() {
  const video = document.getElementById('video');
  if (!video) return;
  if (cameraReady) return;

  ensureStatusBox();
  setCameraStatus('Requesting camera access...');

  navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
    .then(stream => {
      video.srcObject = stream;
      video.onloadedmetadata = () => {
        video.play().catch(() => {});
        cameraReady = true;
        setCameraStatus('Camera is ready.');
      };
    })
    .catch(err => {
      cameraReady = false;
      setCameraStatus('Camera access was blocked. Allow camera permission and refresh the page.', true);
      console.error(err);
    });
}

function captureFrame() {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  if (!video || !canvas) return null;

  if (!cameraReady && !(video.readyState >= 2)) {
    setCameraStatus('Camera is still starting. Please wait a moment and try again.', true);
    return null;
  }

  const width = video.videoWidth || 640;
  const height = video.videoHeight || 480;
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, width, height);
  setCameraStatus('Image captured.');
  return canvas.toDataURL('image/jpeg', 0.9);
}

function showLoader(show) {
  const loader = document.getElementById('loader');
  if (loader) loader.style.display = show ? 'block' : 'none';
}
