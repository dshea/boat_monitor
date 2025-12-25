<?php
// upload_json.php
// Accept a JSON upload via POST (multipart/form-data, field `file`) or
// via PUT (raw body). Saves the file into the same directory as this script
// so `readJson.php` can pick it up and import it.

function respond($code, $data) {
    http_response_code($code);
    header('Content-Type: application/json');
    echo json_encode($data);
    exit;
}

$dest_dir = __DIR__ . DIRECTORY_SEPARATOR;

// sanitize a filename (keep only safe chars)
function safe_filename($name) {
    $name = basename($name);
    $name = preg_replace('/[^A-Za-z0-9._-]/', '_', $name);
    return $name;
}

// generate a default filename
function default_filename() {
    return date('Y-m-d_T_H-i-s') . '.json';
}

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'POST') {
    if (!isset($_FILES['file'])) {
        respond(400, ['status' => 'error', 'message' => 'No file field in POST (expected `file`)']);
    }

    $f = $_FILES['file'];
    if ($f['error'] !== UPLOAD_ERR_OK) {
        respond(400, ['status' => 'error', 'message' => 'Upload error code: ' . $f['error']]);
    }

    $orig = isset($f['name']) ? $f['name'] : default_filename();
    $name = safe_filename($orig);
    $target = $dest_dir . $name;

    if (!move_uploaded_file($f['tmp_name'], $target)) {
        respond(500, ['status' => 'error', 'message' => 'Failed to move uploaded file']);
    }

    // validate JSON
    $content = file_get_contents($target);
    $json = json_decode($content);
    if ($json === null && json_last_error() !== JSON_ERROR_NONE) {
        // remove invalid file to avoid clutter
        @unlink($target);
        respond(400, ['status' => 'error', 'message' => 'Invalid JSON: ' . json_last_error_msg()]);
    }

    respond(200, ['status' => 'ok', 'filename' => $name]);

} else if ($method === 'PUT') {
    // read raw body
    $body = file_get_contents('php://input');
    if ($body === false || strlen($body) === 0) {
        respond(400, ['status' => 'error', 'message' => 'Empty PUT body']);
    }

    // choose filename from query param or default
    $name = isset($_GET['filename']) ? safe_filename($_GET['filename']) : default_filename();
    $target = $dest_dir . $name;

    if (file_put_contents($target, $body) === false) {
        respond(500, ['status' => 'error', 'message' => 'Failed to write file']);
    }

    // validate JSON
    $json = json_decode($body);
    if ($json === null && json_last_error() !== JSON_ERROR_NONE) {
        @unlink($target);
        respond(400, ['status' => 'error', 'message' => 'Invalid JSON: ' . json_last_error_msg()]);
    }

    respond(200, ['status' => 'ok', 'filename' => $name]);

} else {
    respond(405, ['status' => 'error', 'message' => 'Method not allowed']);
}

?>
