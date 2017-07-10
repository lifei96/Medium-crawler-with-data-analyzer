function draw_comm()
    Y = [382397, 119854, 114353, 78939, 68793, 62981, 42316, 34748, 25183, 24754];
    X = {'1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th'};
    bar(Y, 0.6, 'k');
    xlim([0.5 10.5])
    set(gca, 'xticklabel', X);
    set(gca, 'FontSize', 12);
    xlabel('Top 10 Communities','FontSize',20);
    ylabel('Community Size','FontSize',20);
    title('');
    grid off;
    print('./results/graph/comm.eps', '-depsc')
end