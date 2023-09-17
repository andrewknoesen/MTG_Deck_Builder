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

    componentDidMount() {
        // Calculate the boundaries of the parent div after the component is mounted
        this.updateBounds();
        window.addEventListener('resize', this.updateBounds);
    }

    componentWillUnmount() {
        // Clean up the event listener when the component is unmounted
        window.removeEventListener('resize', this.updateBounds);
    }

    updateBounds = () => {
        if (this.cardRef.current) {
            const parentDiv = this.cardRef.current.parentElement;
            const parentRect = parentDiv.getBoundingClientRect();

            // Calculate the boundaries for the Draggable component
            const bounds = {
                left: parentRect.left,
                top: parentRect.top,
                right: parentRect.right - this.state.width,
                bottom: parentRect.bottom - this.state.height,
            };

            this.setState({ bounds });
        }
    };

    handleDrag = (e, ui) => {
        this.setState({
            x: ui.x,
            y: ui.y,
        });
    };

    handleResize = (e, direction, ref, delta, position) => {
        const newWidth = parseFloat(ref.style.width);
        const newHeight = newWidth * (360 / 200); // Maintain the aspect ratio (width:height = 200:360)

        this.setState({
            width: newWidth,
            height: newHeight,
            ...position,
        });

        this.updateBounds(); // Update the bounds after resizing
    };

    render() {
        const { width, height, x, y, bounds } = this.state;
        const gridX = width * 1.1; // 110% of the image size (width)

        return (
            <Draggable
                nodeRef={this.cardRef} // Use the ref here
                handle=".resize-handle"
                grid={[gridX, 10]}
                onDrag={this.handleDrag}
                position={{ x, y }}
                bounds={bounds} // Set the bounds for restricting movement
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
