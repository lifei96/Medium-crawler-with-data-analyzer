function draw_paths()
    Y = [0, 28014986, 5877418361, 111830807342, 286847846941, 204059927677, 63267565958, 11340749602, 1539082032, 199971465, 24575845, 2372517, 178665, 13228, 1038, 57, 2];
    Y_sum = sum(Y);
    Y = Y./Y_sum;
    X = 0:length(Y)-1;
    disp(sum(X.*Y));
    plot(X, Y, '-k.', 'markers', 24, 'LineWidth', 2);
    set(gca,'XTick',(0:4:16))
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Path Length','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/graph/paths.eps', '-depsc')
end