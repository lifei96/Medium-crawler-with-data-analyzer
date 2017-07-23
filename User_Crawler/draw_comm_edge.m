function draw_comm_edge()
    Y = [6.15840343936,6.31438008143; 22.3919101574,31.9919985983; 27.7569718328,36.6208844543; 14.7598018723,4.44557189729; 53.8770369078,64.6455017226; 31.6768866801,63.5480065417; 14.6347953493,13.5021268551; 12.0719753655,12.7105732704; 11.1443434063,5.71091609419; 16.029772966,40.0776844146];
    X = {'1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th'};
    bar(Y, 1);
    colormap(copper);
    xlim([0.5 10.5]);
    ylim([0 80]);
    set(gca, 'xticklabel', X);
    set(gca, 'FontSize', 12);
    xlabel('Top 10 Communities','FontSize',20);
    ylabel('Avg. Number of Degree','FontSize',20);
    legend('Avg. Intra-Community Degree', 'Avg. Inter-Community Degree');
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/graph/comm_edge.eps', '-depsc')
end