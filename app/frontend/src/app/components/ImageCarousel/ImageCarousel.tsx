import config from '@app/config';
import * as React from 'react';
import ImageGallery from "react-image-gallery";


interface Image {
    image_name: string;
    image_key: string;
}

interface ImageCarouselProps {
    images: Image[];
}

const ImageCarousel: React.FunctionComponent<ImageCarouselProps> = ({ images }) => {
    const transformedImages = images.map(image => ({
        original: "/images/" + image.image_key,
        thumbnail: "/images/" + image.image_key,
        thumbnailClass: "image-gallery-thumbnail",
        originalClass: "image-gallery-original",
        originalAlt: image.image_key,
        thumbnailAlt: image.image_key,
    }));
    console.log("transformed images: " + transformedImages);
    return (
        <ImageGallery items={transformedImages} />
    );
}

export { ImageCarousel };
