export function Base64Encode(data) {
    return btoa(encodeURIComponent(data).replace(/%([0-9A-F]{2})/g, function(match, p1) {
        return String.fromCharCode(parseInt(p1, 16))
    }))
}
