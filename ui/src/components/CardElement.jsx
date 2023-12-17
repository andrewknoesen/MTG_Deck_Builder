import React from 'react';
import Draggable from 'react-draggable';

const imageUrl = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRe7Ki-ys2G_MMb_xCrY7nAf87F5ZiIOyCh4f5H_JCTTtMSMLCL';

export default class CardElement extends React.Component {
    constructor(props) {
        super(props);
        this.cardRef = React.createRef(); // Create a ref to access the DOM element
        this.state = {
            width: 200,
            height: 360,
            x: 0,
            y: 0,
        };
    }

    handleDrag = (e, ui) => {
        this.setState({
            x: ui.x,
            y: ui.y,
        });
    };

    
    render() {
        const { width, height, x, y } = this.state;
        const gridX = width * 1.1; // 110% of the image size (width)
        const gridY = height * 0.15;

        return (
            <Draggable
                grid={[gridX, gridY]}
                onDrag={this.handleDrag}
                bounds="parent"
            >
                <div
                    ref={this.cardRef} // Use the ref here
                    style={{
                        width: `${width}px`,
                        height: `${height}px`,
                        background: `url(${imageUrl})`,
                        backgroundSize: 'contain',
                        backgroundRepeat: 'no-repeat',
                        position: 'relative',
                    }}
                >
                    <div
                        className="resize-handle"
                        style={{
                            width: '100%',
                            height: '100%',
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            cursor: 'move',
                            zIndex: 1,
                        }}
                    />
                </div>
            </Draggable>
        );
    }
}
